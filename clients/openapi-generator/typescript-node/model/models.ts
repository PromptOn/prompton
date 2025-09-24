import localVarRequest from 'request';

export * from './apiStatusResponse';
export * from './chatGPTChatCompletitionConfig';
export * from './chatGPTChatCompletitionRequest';
export * from './chatGPTChatCompletitionResponse';
export * from './chatGPTCompletitionChoice';
export * from './chatGPTMessage';
export * from './chatGPTRole';
export * from './chatGPTTokenUsage';
export * from './dBStatus';
export * from './hTTPValidationError';
export * from './inferenceCreateByPromptId';
export * from './inferenceCreateByPromptVersionId';
export * from './inferencePostResponse';
export * from './inferenceRead';
export * from './inferenceRequestData';
export * from './inferenceResponseData';
export * from './inferenceResponseError';
export * from './inferenceResponseStatus';
export * from './inferencerequest';
export * from './locationInner';
export * from './loginCredentialsPost';
export * from './orgCreate';
export * from './orgRead';
export * from './orgUpdate';
export * from './promptCreate';
export * from './promptRead';
export * from './promptStatus';
export * from './promptUpdate';
export * from './promptVersionCreate';
export * from './promptVersionProviders';
export * from './promptVersionRead';
export * from './promptVersionStatus';
export * from './promptVersionUpdate';
export * from './response';
export * from './stop';
export * from './token';
export * from './userCreate';
export * from './userRead';
export * from './userRoles';
export * from './validationError';

import * as fs from 'fs';

export interface RequestDetailedFile {
    value: Buffer;
    options?: {
        filename?: string;
        contentType?: string;
    }
}

export type RequestFile = string | Buffer | fs.ReadStream | RequestDetailedFile;


import { ApiStatusResponse } from './apiStatusResponse';
import { ChatGPTChatCompletitionConfig } from './chatGPTChatCompletitionConfig';
import { ChatGPTChatCompletitionRequest } from './chatGPTChatCompletitionRequest';
import { ChatGPTChatCompletitionResponse } from './chatGPTChatCompletitionResponse';
import { ChatGPTCompletitionChoice } from './chatGPTCompletitionChoice';
import { ChatGPTMessage } from './chatGPTMessage';
import { ChatGPTRole } from './chatGPTRole';
import { ChatGPTTokenUsage } from './chatGPTTokenUsage';
import { DBStatus } from './dBStatus';
import { HTTPValidationError } from './hTTPValidationError';
import { InferenceCreateByPromptId } from './inferenceCreateByPromptId';
import { InferenceCreateByPromptVersionId } from './inferenceCreateByPromptVersionId';
import { InferencePostResponse } from './inferencePostResponse';
import { InferenceRead } from './inferenceRead';
import { InferenceRequestData } from './inferenceRequestData';
import { InferenceResponseData } from './inferenceResponseData';
import { InferenceResponseError } from './inferenceResponseError';
import { InferenceResponseStatus } from './inferenceResponseStatus';
import { Inferencerequest } from './inferencerequest';
import { LocationInner } from './locationInner';
import { LoginCredentialsPost } from './loginCredentialsPost';
import { OrgCreate } from './orgCreate';
import { OrgRead } from './orgRead';
import { OrgUpdate } from './orgUpdate';
import { PromptCreate } from './promptCreate';
import { PromptRead } from './promptRead';
import { PromptStatus } from './promptStatus';
import { PromptUpdate } from './promptUpdate';
import { PromptVersionCreate } from './promptVersionCreate';
import { PromptVersionProviders } from './promptVersionProviders';
import { PromptVersionRead } from './promptVersionRead';
import { PromptVersionStatus } from './promptVersionStatus';
import { PromptVersionUpdate } from './promptVersionUpdate';
import { Response } from './response';
import { Stop } from './stop';
import { Token } from './token';
import { UserCreate } from './userCreate';
import { UserRead } from './userRead';
import { UserRoles } from './userRoles';
import { ValidationError } from './validationError';

/* tslint:disable:no-unused-variable */
let primitives = [
                    "string",
                    "boolean",
                    "double",
                    "integer",
                    "long",
                    "float",
                    "number",
                    "any"
                 ];

let enumsMap: {[index: string]: any} = {
        "ChatGPTRole": ChatGPTRole,
        "InferenceResponseStatus": InferenceResponseStatus,
        "PromptStatus": PromptStatus,
        "PromptVersionProviders": PromptVersionProviders,
        "PromptVersionStatus": PromptVersionStatus,
        "UserRoles": UserRoles,
}

let typeMap: {[index: string]: any} = {
    "ApiStatusResponse": ApiStatusResponse,
    "ChatGPTChatCompletitionConfig": ChatGPTChatCompletitionConfig,
    "ChatGPTChatCompletitionRequest": ChatGPTChatCompletitionRequest,
    "ChatGPTChatCompletitionResponse": ChatGPTChatCompletitionResponse,
    "ChatGPTCompletitionChoice": ChatGPTCompletitionChoice,
    "ChatGPTMessage": ChatGPTMessage,
    "ChatGPTTokenUsage": ChatGPTTokenUsage,
    "DBStatus": DBStatus,
    "HTTPValidationError": HTTPValidationError,
    "InferenceCreateByPromptId": InferenceCreateByPromptId,
    "InferenceCreateByPromptVersionId": InferenceCreateByPromptVersionId,
    "InferencePostResponse": InferencePostResponse,
    "InferenceRead": InferenceRead,
    "InferenceRequestData": InferenceRequestData,
    "InferenceResponseData": InferenceResponseData,
    "InferenceResponseError": InferenceResponseError,
    "Inferencerequest": Inferencerequest,
    "LocationInner": LocationInner,
    "LoginCredentialsPost": LoginCredentialsPost,
    "OrgCreate": OrgCreate,
    "OrgRead": OrgRead,
    "OrgUpdate": OrgUpdate,
    "PromptCreate": PromptCreate,
    "PromptRead": PromptRead,
    "PromptUpdate": PromptUpdate,
    "PromptVersionCreate": PromptVersionCreate,
    "PromptVersionRead": PromptVersionRead,
    "PromptVersionUpdate": PromptVersionUpdate,
    "Response": Response,
    "Stop": Stop,
    "Token": Token,
    "UserCreate": UserCreate,
    "UserRead": UserRead,
    "ValidationError": ValidationError,
}

export class ObjectSerializer {
    public static findCorrectType(data: any, expectedType: string) {
        if (data == undefined) {
            return expectedType;
        } else if (primitives.indexOf(expectedType.toLowerCase()) !== -1) {
            return expectedType;
        } else if (expectedType === "Date") {
            return expectedType;
        } else {
            if (enumsMap[expectedType]) {
                return expectedType;
            }

            if (!typeMap[expectedType]) {
                return expectedType; // w/e we don't know the type
            }

            // Check the discriminator
            let discriminatorProperty = typeMap[expectedType].discriminator;
            if (discriminatorProperty == null) {
                return expectedType; // the type does not have a discriminator. use it.
            } else {
                if (data[discriminatorProperty]) {
                    var discriminatorType = data[discriminatorProperty];
                    if(typeMap[discriminatorType]){
                        return discriminatorType; // use the type given in the discriminator
                    } else {
                        return expectedType; // discriminator did not map to a type
                    }
                } else {
                    return expectedType; // discriminator was not present (or an empty string)
                }
            }
        }
    }

    public static serialize(data: any, type: string) {
        if (data == undefined) {
            return data;
        } else if (primitives.indexOf(type.toLowerCase()) !== -1) {
            return data;
        } else if (type.lastIndexOf("Array<", 0) === 0) { // string.startsWith pre es6
            let subType: string = type.replace("Array<", ""); // Array<Type> => Type>
            subType = subType.substring(0, subType.length - 1); // Type> => Type
            let transformedData: any[] = [];
            for (let index = 0; index < data.length; index++) {
                let datum = data[index];
                transformedData.push(ObjectSerializer.serialize(datum, subType));
            }
            return transformedData;
        } else if (type === "Date") {
            return data.toISOString();
        } else {
            if (enumsMap[type]) {
                return data;
            }
            if (!typeMap[type]) { // in case we dont know the type
                return data;
            }

            // Get the actual type of this object
            type = this.findCorrectType(data, type);

            // get the map for the correct type.
            let attributeTypes = typeMap[type].getAttributeTypeMap();
            let instance: {[index: string]: any} = {};
            for (let index = 0; index < attributeTypes.length; index++) {
                let attributeType = attributeTypes[index];
                instance[attributeType.baseName] = ObjectSerializer.serialize(data[attributeType.name], attributeType.type);
            }
            return instance;
        }
    }

    public static deserialize(data: any, type: string) {
        // polymorphism may change the actual type.
        type = ObjectSerializer.findCorrectType(data, type);
        if (data == undefined) {
            return data;
        } else if (primitives.indexOf(type.toLowerCase()) !== -1) {
            return data;
        } else if (type.lastIndexOf("Array<", 0) === 0) { // string.startsWith pre es6
            let subType: string = type.replace("Array<", ""); // Array<Type> => Type>
            subType = subType.substring(0, subType.length - 1); // Type> => Type
            let transformedData: any[] = [];
            for (let index = 0; index < data.length; index++) {
                let datum = data[index];
                transformedData.push(ObjectSerializer.deserialize(datum, subType));
            }
            return transformedData;
        } else if (type === "Date") {
            return new Date(data);
        } else {
            if (enumsMap[type]) {// is Enum
                return data;
            }

            if (!typeMap[type]) { // dont know the type
                return data;
            }
            let instance = new typeMap[type]();
            let attributeTypes = typeMap[type].getAttributeTypeMap();
            for (let index = 0; index < attributeTypes.length; index++) {
                let attributeType = attributeTypes[index];
                instance[attributeType.name] = ObjectSerializer.deserialize(data[attributeType.baseName], attributeType.type);
            }
            return instance;
        }
    }
}

export interface Authentication {
    /**
    * Apply authentication settings to header and query params.
    */
    applyToRequest(requestOptions: localVarRequest.Options): Promise<void> | void;
}

export class HttpBasicAuth implements Authentication {
    public username: string = '';
    public password: string = '';

    applyToRequest(requestOptions: localVarRequest.Options): void {
        requestOptions.auth = {
            username: this.username, password: this.password
        }
    }
}

export class HttpBearerAuth implements Authentication {
    public accessToken: string | (() => string) = '';

    applyToRequest(requestOptions: localVarRequest.Options): void {
        if (requestOptions && requestOptions.headers) {
            const accessToken = typeof this.accessToken === 'function'
                            ? this.accessToken()
                            : this.accessToken;
            requestOptions.headers["Authorization"] = "Bearer " + accessToken;
        }
    }
}

export class ApiKeyAuth implements Authentication {
    public apiKey: string = '';

    constructor(private location: string, private paramName: string) {
    }

    applyToRequest(requestOptions: localVarRequest.Options): void {
        if (this.location == "query") {
            (<any>requestOptions.qs)[this.paramName] = this.apiKey;
        } else if (this.location == "header" && requestOptions && requestOptions.headers) {
            requestOptions.headers[this.paramName] = this.apiKey;
        } else if (this.location == 'cookie' && requestOptions && requestOptions.headers) {
            if (requestOptions.headers['Cookie']) {
                requestOptions.headers['Cookie'] += '; ' + this.paramName + '=' + encodeURIComponent(this.apiKey);
            }
            else {
                requestOptions.headers['Cookie'] = this.paramName + '=' + encodeURIComponent(this.apiKey);
            }
        }
    }
}

export class OAuth implements Authentication {
    public accessToken: string = '';

    applyToRequest(requestOptions: localVarRequest.Options): void {
        if (requestOptions && requestOptions.headers) {
            requestOptions.headers["Authorization"] = "Bearer " + this.accessToken;
        }
    }
}

export class VoidAuth implements Authentication {
    public username: string = '';
    public password: string = '';

    applyToRequest(_: localVarRequest.Options): void {
        // Do nothing
    }
}

export type Interceptor = (requestOptions: localVarRequest.Options) => (Promise<void> | void);
