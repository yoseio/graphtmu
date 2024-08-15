"use server"

import * as z from "zod";

// Import the Genkit core libraries and plugins.
import { generate } from "@genkit-ai/ai";
import { configureGenkit } from "@genkit-ai/core";
import { defineFlow, runFlow } from "@genkit-ai/flow";
import { vertexAI } from "@genkit-ai/vertexai";

// Import models from the Vertex AI plugin. The Vertex AI API provides access to
// several generative models. Here, we import Gemini 1.5 Flash.
import { gemini15Flash } from "@genkit-ai/vertexai";

configureGenkit({
  plugins: [
    // Load the Vertex AI plugin. You can optionally specify your project ID
    // by passing in a config object; if you don"t, the Vertex AI plugin uses
    // the value from the GCLOUD_PROJECT environment variable.
    vertexAI({ location: "asia-northeast1" }),
  ],
  // Log debug output to tbe console.
  logLevel: "debug",
  // Perform OpenTelemetry instrumentation and enable trace collection.
  enableTracingAndMetrics: true,
});

// Define a simple flow that prompts an LLM to generate menu suggestions.
const menuSuggestionFlow = defineFlow(
  {
    name: "menuSuggestionFlow",
    inputSchema: z.string(),
    outputSchema: z.string(),
  },
  async (subject) => {
    // Construct a request and send it to the model API.
    const llmResponse = await generate({
      prompt: `Suggest an item for the menu of a ${subject} themed restaurant`,
      model: gemini15Flash,
      config: {
        temperature: 1,
      },
    });

    // Handle the response from the model API. In this sample, we just
    // convert it to a string, but more complicated flows might coerce the
    // response into structured output or chain the response into another
    // LLM call, etc.
    return llmResponse.text();
  }
);

export async function callMenuSuggestionFlow(theme: string) {
  // Invoke the flow. The value you pass as the second parameter must conform to
  // your flow"s input schema.
  const flowResponse = await runFlow(menuSuggestionFlow, theme);
  console.log(flowResponse);
  return flowResponse;
}
