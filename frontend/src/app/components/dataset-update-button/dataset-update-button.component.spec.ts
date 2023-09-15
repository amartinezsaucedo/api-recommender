import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatasetUpdateButtonComponent } from './dataset-update-button.component';

describe('DatasetUpdateButtonComponent', () => {
  let component: DatasetUpdateButtonComponent;
  let fixture: ComponentFixture<DatasetUpdateButtonComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DatasetUpdateButtonComponent]
    });
    fixture = TestBed.createComponent(DatasetUpdateButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
