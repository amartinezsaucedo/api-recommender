import {Component, Input, OnChanges, SimpleChanges} from '@angular/core';
import {Metadata} from "../../../../models/metadata";
import {ifChanged} from "../../../../utils/props";
import {Recommendation} from "../../../../models/recommendations";

@Component({
  selector: 'app-recommendation-list',
  templateUrl: './recommendation-list.component.html',
  styleUrls: ['./recommendation-list.component.sass']
})
export class RecommendationListComponent implements OnChanges{
  @Input() recommendations: Recommendation[] = [];
  @Input() query: string = "";
  @Input() metadata: Metadata = new Metadata();

  constructor() {
  }

  ngOnChanges(changes: SimpleChanges) {
    ifChanged(changes['recommendations'], () => this.recommendations = changes['recommendations'].currentValue);
    ifChanged(changes['query'], () => this.query = changes['query'].currentValue);
    ifChanged(changes['metadata'], () => this.metadata = changes['metadata'].currentValue);
  }
}
