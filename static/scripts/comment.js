function disableButton(event) {
  event.target.querySelector("button").disabled = true;
}

document.addEventListener("alpine:init", () => {
    Alpine.store("commentCount", {
      count: 1,
      increment() {
        this.count++;
      },
    });
});

function commentCountComponent(initialCount) {
  return {
    init() {
      this.$store.commentCount.count = initialCount
    }
  }

}