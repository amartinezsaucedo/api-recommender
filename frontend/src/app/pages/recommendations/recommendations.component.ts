import {Component, inject} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {RecommendationService} from "../../services/recommendation-service";
import {Recommendations} from "../../models/recommendations";

@Component({
  selector: 'app-recommendations',
  templateUrl: './recommendations.component.html',
  styleUrls: ['./recommendations.component.sass'],
  providers: [RecommendationService],
})
export class RecommendationsComponent {
  queryForm = new FormGroup({
    query: new FormControl('', Validators.required),
    algorithm: new FormControl('', Validators.required),
    model: new FormControl('', Validators.required)
  });
  loading = false;
  private service = inject(RecommendationService);
  recommendations: Recommendations = new Recommendations();
  queryValue: string = ""

  get query() {
    return this.queryForm.get("query");
  }

  get algorithm() {
    return this.queryForm.get("algorithm");
  }

  get model() {
    return this.queryForm.get("model");
  }

  onSubmit() {
    this.loading = true;
    this.recommendations = new Recommendations();
    this.queryValue = <string>this.query?.value;
    this.service.getRecommendations(<string>this.query?.value, <string>this.algorithm?.value, <string>this.model?.value)
      .subscribe(recommendations => {
        this.loading = false;
        this.recommendations = recommendations;
      })
  }

  getAlgorithm(value: string) {
    this.queryForm.patchValue({algorithm: value});
  }

  getModel(value: string) {
    this.queryForm.patchValue({model: value});
  }
}