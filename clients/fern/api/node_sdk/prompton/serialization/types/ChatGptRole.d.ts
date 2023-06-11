/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "..";
import * as PromptonApi from "../../api";
import * as core from "../../core";
export declare const ChatGptRole: core.serialization.Schema<serializers.ChatGptRole.Raw, PromptonApi.ChatGptRole>;
export declare namespace ChatGptRole {
    type Raw = "system" | "user" | "assistant";
}