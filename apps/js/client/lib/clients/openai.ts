import OpenAI from "openai/index.mjs";

import { OPENAI_API_KEY } from "@/lib/constants";

export const OpenAIClient = new OpenAI({
  apiKey: OPENAI_API_KEY,
});
