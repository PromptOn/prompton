/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as PromptonApi from "..";
export interface InferenceResponseError {
    completedAt?: string;
    completitionDurationSeconds?: number;
    isClientConnectedAtFinish?: boolean;
    isError?: boolean;
    error: PromptonApi.InferenceError;
}
