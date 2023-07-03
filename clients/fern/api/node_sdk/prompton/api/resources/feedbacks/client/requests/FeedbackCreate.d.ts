/**
 * This file was auto-generated by Fern from our API Definition.
 */
export interface FeedbackCreate {
    /** The inference being rated */
    inferenceId: string;
    /** API consumers' end user id If feedback from end user otherwise null */
    endUserId?: string;
    /** Specifies which part of the output the feedback is about. Can be used when the inference has multiple sections which require separate feedback */
    feedbackForPart?: string;
    /** Any integer score. Rules are up to the API consumer. Can be null if it was flagging or note only */
    score?: number;
    /** Any string when inference was flagged. Can be null if it is scoring or note only */
    flag?: string;
    note?: string;
    metadata?: Record<string, unknown>;
}