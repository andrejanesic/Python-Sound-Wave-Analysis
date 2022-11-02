TEXT_WELCOME = """
   ____                 __     ____                  __
  / __/__  ___ ___ ____/ /    / __/__  __ _____  ___/ /
 _\ \/ _ \/ -_) -_) __/ _ \  _\ \/ _ \/ // / _ \/ _  / 
/___/ .__/\__/\__/\__/_//_/_/___/\___/\_,_/_//_/\_,_/  
   /_/    / _ | ___  ___ _/ /_ _____ ___ ____          
         / __ |/ _ \/ _ `/ / // /_ // -_) __/          
        /_/ |_/_//_/\_,_/_/\_, //__/\__/_/             
                          /___/                        

"""
TEXT_CLEAN = "✂️  cut <filename> [...filenames] ::: Removes non-speech parts of the selected soundwaves"
TEXT_HELP = "📜 help ::: Shows this menu."
TEXT_LIST = "💿 list [like] ::: Lists all loaded wavefiles. Optionally, list all waves with [like] in their name"
TEXT_LOAD = "📥 load <filename> [...filenames] ::: Loads each specified file from ./input/<filename>.wav"
TEXT_PLOT = "📈 plot [waveform|spectogram|histogram] [...filenames] ::: Plots the selected wavefile on the selected type of graph. Multiple wavefiles may be plotted. If no file is specified, plots all loaded."
TEXT_QUIT = "🚪 quit ::: Closes the application"
TEXT_NOT_LOADED = "🤔 I couldn't find this sound wave, did you load it? "
TEXT_INVALID_SYNTAX = "🤔 I couldn't understand that. Try this command:"
TEXT_GENERATE = "🎧 gen [name] [harmonics] [duration] ::: Generates a sound wave with the given name and number of harmonics, lasting [duration] ms. If no name provided, name will be generated. Harmonics number equals 10 by default. Duration equals 100 (ms) by default."
TEXT_ERROR_WRITING = "❌ There was an error while saving the wave "
TEXT_GENERATED = "💽 You're officially an artist. Here's your sound wave: "
TEXT_PLOTTING = "📈 Plotting..."
