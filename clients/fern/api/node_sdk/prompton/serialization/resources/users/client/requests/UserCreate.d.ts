/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "../../../..";
import * as PromptonApi from "../../../../../api";
import * as core from "../../../../../core";
export declare const UserCreate: core.serialization.Schema<serializers.UserCreate.Raw, PromptonApi.UserCreate>;
export declare namespace UserCreate {
    interface Raw {
        full_name?: string | null;
        disabled?: boolean | null;
        role?: serializers.UserRoles.Raw | null;
        org_id: string;
        email: string;
        plain_password: string;
    }
}