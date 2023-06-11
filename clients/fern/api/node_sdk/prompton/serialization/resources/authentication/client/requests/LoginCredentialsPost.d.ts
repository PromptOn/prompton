/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "../../../..";
import * as PromptonApi from "../../../../../api";
import * as core from "../../../../../core";
export declare const LoginCredentialsPost: core.serialization.Schema<serializers.LoginCredentialsPost.Raw, PromptonApi.LoginCredentialsPost>;
export declare namespace LoginCredentialsPost {
    interface Raw {
        username: string;
        password: string;
    }
}