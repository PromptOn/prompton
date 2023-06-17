export * from './authenticationApi';
import { AuthenticationApi } from './authenticationApi';
export * from './defaultApi';
import { DefaultApi } from './defaultApi';
export * from './inferencesApi';
import { InferencesApi } from './inferencesApi';
export * from './orgsApi';
import { OrgsApi } from './orgsApi';
export * from './promptVersionsApi';
import { PromptVersionsApi } from './promptVersionsApi';
export * from './promptsApi';
import { PromptsApi } from './promptsApi';
export * from './serverStatusApi';
import { ServerStatusApi } from './serverStatusApi';
export * from './usersApi';
import { UsersApi } from './usersApi';
import * as http from 'http';

export class HttpError extends Error {
    constructor (public response: http.IncomingMessage, public body: any, public statusCode?: number) {
        super('HTTP request failed');
        this.name = 'HttpError';
    }
}

export { RequestFile } from '../model/models';

export const APIS = [AuthenticationApi, DefaultApi, InferencesApi, OrgsApi, PromptVersionsApi, PromptsApi, ServerStatusApi, UsersApi];
