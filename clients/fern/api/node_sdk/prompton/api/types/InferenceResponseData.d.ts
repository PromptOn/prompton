/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as PromptonApi from "..";
export interface InferenceResponseData {
    completedAt?: string;
    completitionDurationSeconds?: number;
    isClientConnectedAtFinish?: boolean;
    isError?: boolean;
    tokenUsage: PromptonApi.ChatGptTokenUsage;
    rawResponse: PromptonApi.ChatGptChatCompletitionResponse;
}
