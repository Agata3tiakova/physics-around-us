function animationClassesFor(target) {
  if (target === "all") return ["play-cat", "play-box"];
  if (target === "falling_box") return ["play-box"];
  if (target === "jumping_cat") return ["play-cat"];
  return [];
}

export default function renderPhysicsScene(component) {
  const { data: level, parentElement, setTriggerValue } = component;
  const scene = parentElement.querySelector("#scene");

  if (!scene) return;
  scene.innerHTML = "";
  scene.className = "";
  if (level.id === "kitchen_01") scene.classList.add("kitchen-scene");
  if (level.id === "study_room_01") scene.classList.add("study-scene");
  scene.setAttribute("aria-label", level.scene_label || "Interactive physics scene");

  const background = document.createElement("img");
  background.className = "scene-background";
  background.alt = level.scene_alt || level.title;
  background.src = level.background_data_url;
  background.draggable = false;
  scene.appendChild(background);

  const sprites = level.sprite_data_urls || {};
  [
    ["box", sprites.box, "Box falling from the shelf"],
    ["soup-pot", sprites.soup_pot, "Pot of hot soup"],
    ["steam", sprites.steam, "Steam rising from the soup"],
    ["kettle", sprites.kettle, "Electric kettle"],
  ].forEach(([className, source, alt]) => {
    if (!source) return;
    const image = document.createElement("img");
    image.className = `scene-object ${className}`;
    image.src = source;
    image.alt = alt;
    image.draggable = false;
    scene.appendChild(image);
  });

  [
    ["cat-floor", sprites.cat_floor, "Cat sitting on the floor"],
    ["cat-jumping", sprites.cat_jumping, "Cat jumping"],
    ["cat-table", sprites.cat_table, "Cat sitting on the counter"],
  ].forEach(([className, source, alt]) => {
    if (!source) return;
    const image = document.createElement("img");
    image.className = `scene-object cat-pose ${className}`;
    image.src = source;
    image.alt = alt;
    image.draggable = false;
    scene.appendChild(image);
  });

  const legend = document.createElement("div");
  legend.className = "legend";
  legend.textContent = level.legend || "Find a physical phenomenon";
  scene.appendChild(legend);

  (level.objects || []).forEach((object) => {
    const button = document.createElement("button");
    button.className = `hotspot ${object.id}`;
    button.type = "button";
    button.title = object.label;
    button.setAttribute("aria-label", object.label);
    button.style.left = `${object.position.x}%`;
    button.style.top = `${object.position.y}%`;
    button.style.width = `${object.size.width}%`;
    button.style.height = `${object.size.height || 16}%`;
    if (object.id === level.active_object_id) button.classList.add("selected");
    button.onclick = () => {
      const eventToken = `${Date.now()}-${object.id}`;
      scene.querySelectorAll(".hotspot").forEach((item) => item.classList.remove("selected"));
      button.classList.add("selected");
      setTriggerValue("selected", { object_id: object.id, replay_token: eventToken });
    };
    scene.appendChild(button);
  });

  const replayToken = String(level.replay_token || "0");
  const storageKey = `physics-scene:${level.id}:last-replay`;
  const lastReplayToken = sessionStorage.getItem(storageKey);
  const finishedObjectIds = new Set(level.finished_object_ids || []);
  const animationClasses = animationClassesFor(level.animation_target);
  const shouldReplay =
    animationClasses.length && replayToken !== "0" && replayToken !== lastReplayToken;
  if (finishedObjectIds.has("jumping_cat")) scene.classList.add("cat-finished");
  if (finishedObjectIds.has("falling_box")) scene.classList.add("box-finished");

  (level.objects || []).forEach((object) => {
      if (shouldReplay && (level.animation_target === "all" || level.animation_target === object.id)) return;
      if (!finishedObjectIds.has(object.id) || !object.finished_position) return;
      const button = scene.querySelector(`.hotspot.${object.id}`);
      if (!button) return;
      button.style.left = `${object.finished_position.x}%`;
      button.style.top = `${object.finished_position.y}%`;
  });

  if (shouldReplay) {
    scene.classList.add(...animationClasses);
    sessionStorage.setItem(storageKey, replayToken);
  }
}
