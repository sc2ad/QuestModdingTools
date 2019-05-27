# QuestModdingTools

Provides a few tools that will (hopefully) aid in the ability to modify/replace/create custom songs

# Tutorial for Creating a Custom Song in an existing collection

Please note that this tutorial has yet to be fully ironed out, nor does this work for entirely custom songs.

Instead, I will guide you through the process of:

1. Adding your "own" custom song (referred to as level) to .assets
2. Adding this song to existing collections in .assets
3. Recompiling this .assets file
4. Profit

## Initial Preparations
Before we can even start, please make sure you have access to the `sharedassets17.assets.split*` files. These files can be found in the `assets\bin\Data` folder of the beat saber apk. Next, please clone/download this repo, as well as download the zip from the releases page.

Also make sure you have python >= 3 on your computer. You can check your version of python by doing `python --version`.

I would also recommend moving all of the `sharedassets17.assets.split*` files out of the apk directory to somewhere more useful/easier to access, as well as making backups.

## Begin!
1. First off, we want to turn our several `.split` files into one, big `.assets` file. We can do this via the following python command: `python splitter.py "path/to/sharedassets17.assets.split" 1`. This will create a `sharedassets17.assets` file in the directory `path/to/`.
2. Next, we want to make our `.assets` file legible. We can do this by converting only pieces of information that we care about to JSON, via the following command: `python replacer.py "path/to/sharedassets17.assets" --json-out "LegibleData"`. This will create a directory called `LegibleData` in the directory that you were in when you ran that command. Inside this directory contains 3 subfolders:
- `LevelCollections`
- `LevelPacks`
- `SongLevels`
It is important to **NOT** delete or rename these directories, as it looks for _exactly_ these names. Inside each of these directories, there are .json files for each object under each directory.
3. We can edit these .json files however we prefer, however, make sure that you increase the size of your arrays when you add or remove elements.
4. Now that we have our legible data, let us create our own level to add to a collection. You can do this by copy-pasting an existing level from the `SongLevels` folder, or by using `MyOwnCustomNameY.json` from the .zip from the releases page.
5. Do **NOT** save this new .json file in the `LegibleData` directory, or the `SongLevels` directory! Save it somewhere else, it will appear once you have added it successfully.
6. A Custom Object must have two JSON keys:
- `Metadata`
- `Data`

`Metadata` must be a dictionary with at least two items:
- `ByteSize`: The size of the file in bytes. This is tricky to calculate (this step will be automated in the future)
- `TypeID`: The type ID of the object. The type ID of a level is `15`.

`Data` must be a dictionary containing a raw .json from `LegibleData`. It must contain at least the following 4 values:
- `GameObject`: A dict that represents an object pointer. Must contain at least two keys: `FileID` and `PathID`
- `Enabled`: A uint32 that represents the enabled state of the object.
- `MonoScript`: A dict that represents an object pointer. Must contain at least two keys: `FileID` and `PathID`
- `Name`: An aligned_string that represents the name of the object.

If you copied over an existing level to make your own, rejoice! You won't have to find all of those annoying parameters...

Otherwise, get searching for `MonoScript.PathID` (which represents the script in charge of this object)

7. After creating your custom object (or copying it and changing a few things) make sure that your `ByteSize` is correct (to do this, I usually copy over an existing level that has a known `ByteSize` and then make changes and carefully count how many bytes I have added/removed.)
8. Now we are ready to add the custom object to our `.assets` file! Run the following command: `python replacer.py "path/to/sharedassets17.assets" --json-out "LegibleData" --add-object "myCustomObject.json"` If all goes well (and you gave your custom object a unique name) you should see your custom song appear in the `SongLevels` folder. Nicely done!
9. Now let's add it to a collection. Find the `ExtrasLevelCollection.json` and increase the size of the array and add a new element. Refer to your custom object in the `LegibleData` folder in order to find your `PathID`.
10. Now we can build everything back! Run the following command: `python replacer.py "path/to/sharedassets17.assets" --json-in "LegibleData" --output "sharedassets17.assets.split" --add-object "myCustomSong.json"`. You will find many `sharedassets17.assets.split*` files in the directory that you ran this command in, which you can now copy over to the .apk.
11. Repackage and sign the apk, install it, and enjoy viewing your new song! (Even if it already exists under a different name...)
