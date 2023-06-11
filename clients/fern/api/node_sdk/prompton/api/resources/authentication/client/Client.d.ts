/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as core from "../../../../core";
import * as PromptonApi from "../../..";
export declare namespace Authentication {
    interface Options {
        environment: string;
        token?: core.Supplier<core.BearerToken | undefined>;
    }
}
export declare class Authentication {
    protected readonly options: Authentication.Options;
    constructor(options: Authentication.Options);
    /**
     * @throws {@link PromptonApi.BadRequestError}
     * @throws {@link PromptonApi.UnauthorizedError}
     * @throws {@link PromptonApi.UnprocessableEntityError}
     */
    getAccessTokenExtended(): Promise<PromptonApi.Token>;
    /**
     * Same functionality as /token but taking `username` and `password` args as `application/json` type instead of `application/x-www-form-urlencoded`
     *
     * Don't use it becuase it's a **temporary** workaround for client lib generator and will be removed in the future.
     * @throws {@link PromptonApi.BadRequestError}
     * @throws {@link PromptonApi.UnauthorizedError}
     * @throws {@link PromptonApi.UnprocessableEntityError}
     */
    getAccessToken(request: PromptonApi.LoginCredentialsPost): Promise<PromptonApi.Token>;
    protected _getAuthorizationHeader(): Promise<string | undefined>;
}