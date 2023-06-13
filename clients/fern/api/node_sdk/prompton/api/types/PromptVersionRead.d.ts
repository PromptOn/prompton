/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as PromptonApi from "..";
export interface PromptVersionRead {
    id?: string;
    createdAt?: string;
    createdByUserId?: string;
    createdByOrgId?: string;
    status?: PromptonApi.PromptVersionStatus;
    provider?: PromptonApi.PromptVersionProviders;
    /** <span style="white-space: nowrap">`non-empty`</span> */
    name: string;
    description?: string;
    promptId: string;
    template?: PromptonApi.ChatGptMessage[];
    modelConfig?: PromptonApi.ChatGptChatCompletitionConfig;
    templateArgNames?: string[];
}
