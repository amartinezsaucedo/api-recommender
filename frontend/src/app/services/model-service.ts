import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {catchError, Observable, of} from 'rxjs';
import {Constants} from "../configuration/constants";
import {Model} from "../models/model";

@Injectable()
export class ModelService {
  private modelUrl = 'api/v1/models';

  constructor(private http: HttpClient) {
  }

  getModels(): Observable<Model[]> {
    return this.http.get<Model[]>
    (`${Constants.API_ENDPOINT}${this.modelUrl}`).pipe(catchError(this.handleError<Model[]>('getModels', [])));
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(operation + ": " + error);
      return of(result as T);
    };
  }
}
