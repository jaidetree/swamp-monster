document.addEventListener("DOMContentLoaded", () => {
	const dialog = document.querySelector("[data-lightbox-dialog]")
	if (!dialog) return

	const image = dialog.querySelector("[data-lightbox-image]")
	const closeButton = dialog.querySelector("[data-lightbox-close]")

	document.querySelectorAll("[data-lightbox-trigger]").forEach((trigger) => {
		trigger.addEventListener("click", () => {
			image.src = trigger.dataset.lightboxUrl
			image.alt = trigger.dataset.lightboxAlt || ""
			dialog.showModal()
		})
	})

	closeButton.addEventListener("click", () => dialog.close())

	dialog.addEventListener("click", (event) => {
		if (event.target === dialog) {
			dialog.close()
		}
	})
})
