/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "..";
import * as PromptonApi from "../../api";
import * as core from "../../core";
export declare const NewInferenceRequest: core.serialization.Schema<serializers.NewInferenceRequest.Raw, PromptonApi.NewInferenceRequest>;
export declare namespace NewInferenceRequest {
    type Raw = serializers.InferenceCreateByPromptVersionId.Raw | serializers.InferenceCreateByPromptId.Raw;
}
