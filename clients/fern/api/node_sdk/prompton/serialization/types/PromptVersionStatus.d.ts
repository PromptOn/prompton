/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "..";
import * as PromptonApi from "../../api";
import * as core from "../../core";
export declare const PromptVersionStatus: core.serialization.Schema<serializers.PromptVersionStatus.Raw, PromptonApi.PromptVersionStatus>;
export declare namespace PromptVersionStatus {
    type Raw = "Draft" | "Testing" | "Live" | "Archived";
}
