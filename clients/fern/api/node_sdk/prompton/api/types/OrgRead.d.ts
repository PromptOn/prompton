/**
 * This file was auto-generated by Fern from our API Definition.
 */
export interface OrgRead {
    id?: string;
    createdAt?: string;
    createdByUserId?: string;
    createdByOrgId?: string;
    /** `non-empty` */
    name: string;
    accessKeys?: Record<string, string>;
}