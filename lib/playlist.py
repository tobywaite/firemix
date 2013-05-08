import os
import logging

from lib.json_dict import JSONDict
from lib.preset_loader import PresetLoader

log = logging.getLogger("firemix.lib.playlist")


class Playlist(JSONDict):
    """
    Manages the available presets and the current playlist of presets.
    """

    def __init__(self, app):
        self._app = app
        self._name = app.args.playlist
        self._filepath = os.path.join(os.getcwd(), "data", "playlists", "".join([self._name, ".json"]))
        JSONDict.__init__(self, 'playlist', self._filepath, True)

        self._loader = PresetLoader()
        self._preset_classes = self._loader.load()
        self._playlist_data = self.data.get('playlist', [])
        self._playlist = []

        self._active_index = 0
        self._next_index = 0

        self.generate_playlist()

    def generate_playlist(self):
        if len(self._playlist_data) == 0:
            self._playlist = []

        for entry in self._playlist_data:
            inst = self._preset_classes[entry['classname']](self._app.mixer, name=entry['name'])
            for _, key in enumerate(entry.get('params', {})):
                inst.parameter(key).set(entry['params'][key])
            self._playlist.append(inst)

        self._active_index = 0
        self._next_index = 1 % len(self._playlist)

        return self._playlist

    def save(self):
        log.info("Saving playlist")
        # Pack the current state into self.data
        self.data = {'file-type': 'playlist'}
        playlist = []
        for preset in self._playlist:
            playlist_entry = {'classname': preset.__class__.__name__,
                              'name': preset.get_name()}
            param_dict = {}
            for param in preset.get_parameters():
                param_dict[str(param)] = param.get()
            playlist_entry['params'] = param_dict
            playlist.append(playlist_entry)
        self.data['playlist'] = playlist
        # Superclass write to file
        JSONDict.save(self)

    def get(self):
        return self._playlist

    def advance(self, direction=1):
        """
        Advances the playlist
        """
        self._active_index = (self._active_index + direction) % len(self._playlist)
        self._next_index = (self._next_index + direction) % len(self._playlist)
        self._app.playlist_changed.emit()

    def __len__(self):
        return len(self._playlist)

    def get_active_index(self):
        return self._active_index

    def get_next_index(self):
        return self._next_index

    def get_active_preset(self):
        return self._playlist[self._active_index]

    def get_next_preset(self):
        return self._playlist[self._next_index]

    def get_preset_by_index(self, idx):
        return self._playlist[idx]

    def set_active_index(self, idx):
        self._active_index = idx % len(self._playlist)
        self._next_index = (self._active_index + 1) % len(self._playlist)
        self.get_active_preset()._reset()
        self._app.playlist_changed.emit()

    def set_active_preset_by_name(self, classname):
        for i, preset in enumerate(self._playlist):
            if preset.get_name() == classname:
                self.set_active_index(i)

    def reorder_playlist_by_name(self, names):
        """
        Pass in a list of preset names to reorder.
        """