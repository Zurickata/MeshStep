project(jens)

add_executable (jens


)

#cmake_minimum_required(VERSION 2.6)
project(jens_repair)

#set(CMAKE_BUILD_TYPE Release)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

if(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
  # Update if necessary
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-long-long -pedantic")
endif()

#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin")

set(SOURCE_FILES
        Main
	Point3D
	Hexahedron
	Prism
	Pyramid
	Tetrahedron
	Element
	Quality
	Metric
	MetricJeans
	MetricJens
	MetricJR
	MetricJs
	math/Matrix
    math/Polynom
    math/PolyMatrix
    math/Vector
        )

add_executable(jens ${SOURCE_FILES})


