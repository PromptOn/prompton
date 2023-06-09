/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "../../../..";
import * as PromptonApi from "../../../../../api";
import * as core from "../../../../../core";
export declare const PromptUpdate: core.serialization.Schema<serializers.PromptUpdate.Raw, PromptonApi.PromptUpdate>;
export declare namespace PromptUpdate {
    interface Raw {
        status?: serializers.PromptStatus.Raw | null;
        name?: string | null;
        description?: string | null;
    }
}
