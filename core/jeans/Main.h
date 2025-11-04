/**************************************************************************/
/*                                                                        */
/*                 Main JacStudy                                          */
/*                                                                        */
/**************************************************************************/
/* Allows to display Jacobian Information of a mesh in .m3d format        */
/* Written by Claudio Lobos (clobos@inf.utfsm.cl) 2011					  */
/* UNIVERSIDAD TECNICA FEDERICO SANTA MARIA								  */
/**************************************************************************/

#ifndef Main_h
#define Main_h 1

#include <string>
#include <cctype>
#include <iostream>
#include "../read_write/ReadAnsys.h"
#include "../read_write/ReadM3d.h"
#include "../read_write/WriteAnsys.h"
#include "../read_write/WriteM3d.h"
#include "EnhancedPoint.h"
#include "JacHexahedra.h"
#include "JacPrism.h"
#include "JacTetrahedra.h"
#include "JacPyramid.h"
#include "JacDummy.h"
#include "Invalid.h"
#include <math.h>

#endif

