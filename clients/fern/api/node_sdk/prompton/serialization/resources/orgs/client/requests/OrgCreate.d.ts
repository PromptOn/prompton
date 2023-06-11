/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "../../../..";
import * as PromptonApi from "../../../../../api";
import * as core from "../../../../../core";
export declare const OrgCreate: core.serialization.Schema<serializers.OrgCreate.Raw, PromptonApi.OrgCreate>;
export declare namespace OrgCreate {
    interface Raw {
        name: string;
        access_keys?: Record<string, string> | null;
    }
}
