/**
 * This file was auto-generated by Fern from our API Definition.
 */
export interface OrgCreate {
    /** <span style="white-space: nowrap">`non-empty`</span> */
    name: string;
    accessKeys?: Record<string, string>;
    /** APEX domain for oauth single sign on. Anyone with an email address ending in this domain will be able to register to the org after google account sign in. Only Google OAuth is supported for now. */
    oauthDomain?: string;
}
