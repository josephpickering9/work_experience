/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SlugService {
    /**
     * @returns any Success
     * @throws ApiError
     */
    public static postSlug(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/slug',
        });
    }
}
