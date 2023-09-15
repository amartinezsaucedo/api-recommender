import {Component, inject} from '@angular/core';
import {APIService} from "../../services/api-service";

@Component({
  selector: 'app-dataset-update-button',
  templateUrl: './dataset-update-button.component.html',
  styleUrls: ['./dataset-update-button.component.sass'],
  providers: [APIService]
})
export class DatasetUpdateButtonComponent {
  private apiService = inject(APIService);
  statusUrl: string | null = null;

  updateDataset() {
    this.apiService.updateDataset().subscribe(url => this.statusUrl = url);
  }
}
