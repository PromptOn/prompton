/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "..";
import * as PromptonApi from "../../api";
import * as core from "../../core";
export declare const InferenceCreateByPromptId: core.serialization.ObjectSchema<serializers.InferenceCreateByPromptId.Raw, PromptonApi.InferenceCreateByPromptId>;
export declare namespace InferenceCreateByPromptId {
    interface Raw {
        end_user_id: string;
        source: string;
        template_args?: Record<string, string> | null;
        metadata?: Record<string, unknown> | null;
        request_timeout?: number | null;
        prompt_id: string;
    }
}