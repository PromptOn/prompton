/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "..";
import * as PromptonApi from "../../api";
import * as core from "../../core";
export declare const OrgRead: core.serialization.ObjectSchema<serializers.OrgRead.Raw, PromptonApi.OrgRead>;
export declare namespace OrgRead {
    interface Raw {
        _id?: string | null;
        created_at?: string | null;
        created_by_user_id?: string | null;
        created_by_org_id?: string | null;
        name: string;
        access_keys?: Record<string, string> | null;
    }
}