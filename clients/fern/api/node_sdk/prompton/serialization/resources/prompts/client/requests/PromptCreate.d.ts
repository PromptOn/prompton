/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "../../../..";
import * as PromptonApi from "../../../../../api";
import * as core from "../../../../../core";
export declare const PromptCreate: core.serialization.Schema<serializers.PromptCreate.Raw, PromptonApi.PromptCreate>;
export declare namespace PromptCreate {
    interface Raw {
        status?: serializers.PromptStatus.Raw | null;
        name: string;
        description?: string | null;
    }
}
