/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "..";
import * as PromptonApi from "../../api";
import * as core from "../../core";
export declare const InferenceResponseStatus: core.serialization.Schema<serializers.InferenceResponseStatus.Raw, PromptonApi.InferenceResponseStatus>;
export declare namespace InferenceResponseStatus {
    type Raw = "RequestReceived" | "Processed" | "CompletitionError" | "CompletitionTimeout";
}
