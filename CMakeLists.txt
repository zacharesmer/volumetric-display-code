cmake_minimum_required(VERSION 3.18)
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
project(do_stuff LANGUAGES C CXX ASM)

add_executable(do_stuff be_an_object.c)
set_target_properties(do_stuff PROPERTIES
  CMAKE_C_STANDARD 11
  CMAKE_CXX_STANDARD 17
)

pico_sdk_init()
pico_add_extra_outputs(do_stuff)
target_link_libraries(do_stuff pico_stdlib)