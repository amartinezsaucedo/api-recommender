import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {catchError, Observable, of} from 'rxjs';
import {Constants} from "../configuration/constants";
import {Recommendation} from "../models/recommendations";

@Injectable()
export class RecommendationService {
  private recommendationsUrl = 'api/v1/recommendations';

  constructor(private http: HttpClient) {
  }

  getRecommendations(query: string, algorithm: string, model: string, k: number): Observable<Recommendation[]> {
    return this.http.get<Recommendation[]>
    (`${Constants.API_ENDPOINT}${this.recommendationsUrl}?query=${query}&algorithm=${algorithm}&model=${model}&k=${k}`)
      .pipe(catchError(this.handleError<Recommendation[]>('getRecommendations', [] as Recommendation[])));
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(operation + ": " + error);
      return of(result as T);
    };
  }
}
