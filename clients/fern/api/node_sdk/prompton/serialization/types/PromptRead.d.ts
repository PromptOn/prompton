/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "..";
import * as PromptonApi from "../../api";
import * as core from "../../core";
export declare const PromptRead: core.serialization.ObjectSchema<serializers.PromptRead.Raw, PromptonApi.PromptRead>;
export declare namespace PromptRead {
    interface Raw {
        _id: string;
        created_at: string;
        created_by_user_id: string;
        created_by_org_id: string;
        status: serializers.PromptStatus.Raw;
        name: string;
        description?: string | null;
    }
}
