import {Component, Input, OnChanges, SimpleChanges} from '@angular/core';

@Component({
  selector: 'app-recommendation-list',
  templateUrl: './recommendation-list.component.html',
  styleUrls: ['./recommendation-list.component.sass']
})
export class RecommendationListComponent implements OnChanges{
  @Input() recommendations: string[] = [];
  @Input() query: string = "";
  @Input() metadata: object = {};

  constructor() {
  }

  ngOnChanges(changes: SimpleChanges) {
    this.recommendations = changes['recommendations'].currentValue;
    this.query = changes['query'].currentValue;
    this.metadata = changes['metadata'].currentValue;
  }
}
