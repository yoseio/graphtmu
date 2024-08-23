import OpenAI from "openai";

import { OPENAI_API_KEY } from "@/lib/constants";

export const OpenAIClient = new OpenAI({
  apiKey: OPENAI_API_KEY,
});
