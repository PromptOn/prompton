/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "..";
import * as PromptonApi from "../../api";
import * as core from "../../core";
export declare const InferenceRead: core.serialization.ObjectSchema<serializers.InferenceRead.Raw, PromptonApi.InferenceRead>;
export declare namespace InferenceRead {
    interface Raw {
        _id?: string | null;
        created_at?: string | null;
        created_by_user_id?: string | null;
        created_by_org_id?: string | null;
        end_user_id: string;
        source: string;
        template_args?: Record<string, string> | null;
        metadata?: Record<string, unknown> | null;
        request_timeout?: number | null;
        prompt_version_id: string;
        prompt_id: string;
        prompt_version_name?: string | null;
        status?: serializers.InferenceResponseStatus.Raw | null;
        request?: serializers.InferenceRequestData.Raw | null;
        response?: serializers.InferenceReadResponse.Raw | null;
    }
}