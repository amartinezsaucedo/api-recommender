import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {catchError, map, Observable, of} from 'rxjs';
import {Constants} from "../configuration/constants";
import {Metadata} from "../models/metadata";

@Injectable()
export class APIService {
  private datasetUrl = 'api/v1/dataset';

  constructor(private http: HttpClient) {
  }

  getDatasetInfo(): Observable<Metadata> {
    return this.http.get<Metadata>
    (`${Constants.API_ENDPOINT}${this.datasetUrl}`)
      .pipe(catchError(this.handleError<Metadata>('getDatasetInfo', new Metadata())));
  }

  updateDataset(): Observable<string> {
    return this.http.patch<any>(`${Constants.API_ENDPOINT}${this.datasetUrl}`, {})
      .pipe(map(response => response.headers.get("Location")),
        catchError(this.handleError<string>('updateDataset', '')));
  }

  getDatasetUpdateStatus(url: string): Observable<string> {
    return this.http.get<any>(`${Constants.API_ENDPOINT}${url}`)
      .pipe(map(response => response.headers.get("Location")),
        catchError(this.handleError<string>('getDatasetUpdateStatus', '')));
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(operation + ": " + error);
      return of(result as T);
    };
  }
}
