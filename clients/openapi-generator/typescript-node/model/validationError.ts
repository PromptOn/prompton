/**
 * prompton-api
 * API for prompton - managing full lifecycle of AI chat prompts.
 *
 * The version of the OpenAPI document: 0.0.1
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { RequestFile } from './models';
import { LocationInner } from './locationInner';

export class ValidationError {
    'loc': Array<LocationInner>;
    'msg': string;
    'type': string;

    static discriminator: string | undefined = undefined;

    static attributeTypeMap: Array<{name: string, baseName: string, type: string}> = [
        {
            "name": "loc",
            "baseName": "loc",
            "type": "Array<LocationInner>"
        },
        {
            "name": "msg",
            "baseName": "msg",
            "type": "string"
        },
        {
            "name": "type",
            "baseName": "type",
            "type": "string"
        }    ];

    static getAttributeTypeMap() {
        return ValidationError.attributeTypeMap;
    }
}

