import {SimpleChange} from "@angular/core";

export function ifChanged(prop: SimpleChange,callback: (value: any) => void): void {
  if (prop && prop.currentValue !== undefined) {
    callback(prop.currentValue);
  }
}
