"use strict";
// "Add another date" / "Remove" for the training-request form's repeatable
// target_dates inputs (training.html). Plain DOM cloning from a <template>,
// no framework — matches the vanilla approach in inline_sortable_new.js.
// At least one row always stays: "Remove" no-ops once only one is left.

document.addEventListener("DOMContentLoaded", () => {
  const list = document.querySelector("[data-target-dates-list]");
  const addButton = document.querySelector("[data-add-date]");
  const template = document.querySelector("[data-target-date-template]");
  if (!list || !addButton || !(template instanceof HTMLTemplateElement)) return;

  addButton.addEventListener("click", () => {
    const row = template.content.firstElementChild.cloneNode(true);
    list.appendChild(row);
  });

  list.addEventListener("click", (event) => {
    if (!(event.target instanceof HTMLElement)) return;
    const removeButton = event.target.closest("[data-remove-date]");
    if (!removeButton) return;
    if (list.querySelectorAll("[data-target-date-row]").length <= 1) return;
    removeButton.closest("[data-target-date-row]").remove();
  });
});
