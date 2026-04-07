# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Release")
  file(REMOVE_RECURSE
  "CMakeFiles\\CarTrafficSystem_autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\CarTrafficSystem_autogen.dir\\ParseCache.txt"
  "CarTrafficSystem_autogen"
  )
endif()
