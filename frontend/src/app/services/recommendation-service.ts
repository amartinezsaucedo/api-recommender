import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {catchError, Observable, of} from 'rxjs';
import {Constants} from "../configuration/constants";
import {Recommendations} from "../models/recommendations";

@Injectable()
export class RecommendationService {
  private recommendationsUrl = 'api/v1/recommendations';

  constructor(private http: HttpClient) {
  }

  getRecommendations(query: string, algorithm: string, model: string): Observable<Recommendations> {
    return this.http.get<Recommendations>
    (`${Constants.API_ENDPOINT}${this.recommendationsUrl}?query=${query}&algorithm=${algorithm}&model=${model}`)
      .pipe(catchError(this.handleError<Recommendations>('getRecommendations', {} as Recommendations)));
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(operation + ": " + error);
      return of(result as T);
    };
  }
}
