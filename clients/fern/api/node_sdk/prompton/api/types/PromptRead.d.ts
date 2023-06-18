/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as PromptonApi from "..";
/**
 * Base model for reading from MongoDB. Same as MongoBaseCreate but assumes all DB base fields are populated so generated clients doesn't requrie None checks
 */
export interface PromptRead {
    id: string;
    createdAt: string;
    createdByUserId: string;
    createdByOrgId: string;
    status: PromptonApi.PromptStatus;
    /** <span style="white-space: nowrap">`non-empty`</span> */
    name: string;
    description?: string;
}
