/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as core from "../../../../core";
import * as PromptonApi from "../../..";
export declare namespace Prompts {
    interface Options {
        environment: string;
        token?: core.Supplier<core.BearerToken | undefined>;
    }
}
export declare class Prompts {
    protected readonly options: Prompts.Options;
    constructor(options: Prompts.Options);
    /**
     * @throws {@link PromptonApi.BadRequestError}
     * @throws {@link PromptonApi.UnauthorizedError}
     * @throws {@link PromptonApi.NotFoundError}
     * @throws {@link PromptonApi.UnprocessableEntityError}
     */
    getPromptList(): Promise<PromptonApi.PromptRead[]>;
    /**
     * @throws {@link PromptonApi.BadRequestError}
     * @throws {@link PromptonApi.UnauthorizedError}
     * @throws {@link PromptonApi.UnprocessableEntityError}
     */
    addPrompt(request: PromptonApi.PromptCreate): Promise<unknown>;
    /**
     * @throws {@link PromptonApi.BadRequestError}
     * @throws {@link PromptonApi.UnauthorizedError}
     * @throws {@link PromptonApi.NotFoundError}
     * @throws {@link PromptonApi.UnprocessableEntityError}
     */
    getPromptById(id: string): Promise<PromptonApi.PromptRead>;
    /**
     * @throws {@link PromptonApi.BadRequestError}
     * @throws {@link PromptonApi.UnauthorizedError}
     * @throws {@link PromptonApi.NotFoundError}
     * @throws {@link PromptonApi.UnprocessableEntityError}
     */
    updatePrompt(id: string, request?: PromptonApi.PromptUpdate): Promise<PromptonApi.PromptRead>;
    /**
     * Not implemented
     * @throws {@link PromptonApi.NotFoundError}
     * @throws {@link PromptonApi.UnprocessableEntityError}
     */
    deletePrompt(id: string): Promise<void>;
    protected _getAuthorizationHeader(): Promise<string | undefined>;
}