import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {catchError, Observable, of} from 'rxjs';
import {Constants} from "../configuration/constants";
import {Metadata} from "../models/metadata";

@Injectable()
export class APIService {
  private modelUrl = 'api/v1/dataset';

  constructor(private http: HttpClient) {
  }

  getDatasetInfo(): Observable<Metadata> {
    return this.http.get<Metadata>
    (`${Constants.API_ENDPOINT}${this.modelUrl}`).pipe(catchError(this.handleError<Metadata>('getDatasetInfo', new Metadata())));
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(operation + ": " + error);
      return of(result as T);
    };
  }
}
