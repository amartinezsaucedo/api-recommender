import {Component, inject} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {RecommendationService} from "../../services/recommendation-service";
import {Recommendations} from "../../models/recommendations";
import {APIService} from "../../services/api-service";
import {Metadata} from "../../models/metadata";

@Component({
  selector: 'app-recommendations',
  templateUrl: './recommendations.component.html',
  styleUrls: ['./recommendations.component.sass'],
  providers: [RecommendationService, APIService],
})
export class RecommendationsComponent {
  queryForm = new FormGroup({
    query: new FormControl('', Validators.required),
    algorithm: new FormControl('', Validators.required),
    model: new FormControl('', Validators.required),
    k: new FormControl(10, Validators.required)
  });
  loading = false;
  private recommendationService = inject(RecommendationService);
  private metadataService = inject(APIService);
  recommendations: Recommendations = new Recommendations();
  metadata: Metadata = new Metadata();
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

  get k() {
    return this.queryForm.get("k");
  }

  onSubmit() {
    this.loading = true;
    this.recommendations = new Recommendations();
    this.queryValue = <string>this.query?.value;
    this.metadataService.getDatasetInfo().subscribe(metadata => {
      this.metadata = metadata;
    });
    this.recommendationService.getRecommendations(<string>this.query?.value, <string>this.algorithm?.value, <string>this.model?.value, <number>this.k?.value)
      .subscribe(recommendations => {
        this.loading = false;
        this.recommendations = recommendations;
      });
  }

  getAlgorithm(value: string) {
    this.queryForm.patchValue({algorithm: value});
  }

  getModel(value: string) {
    this.queryForm.patchValue({model: value});
  }

  getK(value: number) {
    this.queryForm.patchValue({k: value});
  }
}
