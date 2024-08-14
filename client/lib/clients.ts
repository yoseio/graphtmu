import { initializeApp, cert, getApps } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore"
import { ExternalAccountClient, GoogleAuth } from "google-auth-library";
import OpenAI from "openai";
import { getVercelOidcToken } from '@vercel/functions/oidc';

import { NullToUndefined } from "@/lib/utils";

const FIREBASE_SA_KEY = process.env["FIREBASE_SA_KEY"] || "";

const GCP_PROJECT_ID = process.env["GCP_PROJECT_ID"] || "";
const GCP_PROJECT_NUMBER = process.env["GCP_PROJECT_NUMBER"] || "";
const GCP_SERVICE_ACCOUNT_EMAIL = process.env["GCP_SERVICE_ACCOUNT_EMAIL"] || "";
const GCP_WORKLOAD_IDENTITY_POOL_ID = process.env["GCP_WORKLOAD_IDENTITY_POOL_ID"] || "";
const GCP_WORKLOAD_IDENTITY_POOL_PROVIDER_ID = process.env["GCP_WORKLOAD_IDENTITY_POOL_PROVIDER_ID"] || "";

const OPENAI_API_KEY = process.env["OPENAI_API_KEY"] || "";

// https://vercel.com/docs/security/secure-backend-access/oidc/gcp
function vercelWorkloadIdentity(
  projectId: string,
  projectNumber: string,
  serviceAccountEmail: string,
  workloadIdentityPoolId: string,
  workloadIdentityPoolProviderId: string,
): GoogleAuth {
  const authClient = NullToUndefined(ExternalAccountClient.fromJSON({
    type: 'external_account',
    audience: `//iam.googleapis.com/projects/${projectNumber}/locations/global/workloadIdentityPools/${workloadIdentityPoolId}/providers/${workloadIdentityPoolProviderId}`,
    subject_token_type: 'urn:ietf:params:oauth:token-type:jwt',
    token_url: 'https://sts.googleapis.com/v1/token',
    service_account_impersonation_url: `https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${serviceAccountEmail}:generateAccessToken`,
    subject_token_supplier: {
      getSubjectToken: getVercelOidcToken,
    },
  }));
  return new GoogleAuth({
    authClient,
    projectId,
  });
}

if (!getApps()?.length) {
  if (FIREBASE_SA_KEY === "") {
    // Workload Identity
    const auth = vercelWorkloadIdentity(
      GCP_PROJECT_ID,
      GCP_PROJECT_NUMBER,
      GCP_SERVICE_ACCOUNT_EMAIL,
      GCP_WORKLOAD_IDENTITY_POOL_ID,
      GCP_WORKLOAD_IDENTITY_POOL_PROVIDER_ID,
    );
    initializeApp({
      credential: {
        getAccessToken: async () => {
          const adc = await auth.getApplicationDefault();
          return {
            access_token: adc.credential.credentials.access_token!,
            expires_in: adc.credential.credentials.expiry_date!,
          }
        },
      }
    });
  } else {
    // Service Account Key
    initializeApp({
      credential: cert(JSON.parse(FIREBASE_SA_KEY))
    });
  }
}
export const FirestoreClient = getFirestore();

export const OpenAIClient = new OpenAI({
  apiKey: OPENAI_API_KEY,
});
