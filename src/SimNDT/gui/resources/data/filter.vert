/*
 * glumpy is an OpenGL framework for the fast visualization of numpy arrays.
 * Copyright (C) 2009-2011  Nicolas P. Rougier. All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * 
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 
 * THIS SOFTWARE IS PROVIDED BY NICOLAS P. ROUGIER ''AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
 * EVENT SHALL NICOLAS P. ROUGIER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 * The views and conclusions contained in the software and documentation are
 * those of the authors and should not be interpreted as representing official
 * policies, either expressed or implied, of Nicolas P. Rougier.
 */
/* #define GRID */
/* #define ELEVATION */
/* #define COLORIZATION */
/* #define INTERPOLATION */
/* #define GAMMA_CORRECTION */


uniform vec2 pixel;
uniform sampler2D texture; /* default location 0 */

#ifdef ELEVATION
uniform float elevation;
#endif

#ifdef GRID
uniform vec4 grid_color;
uniform vec3 grid_size;
uniform vec3 grid_offset;
uniform vec3 grid_thickness;
#endif

#ifdef INTERPOLATION
uniform sampler1D kernel_lut;  /* default location 1 */
#endif

#ifdef COLORIZATION
uniform sampler1D color_lut;   /* default location 2 */
#endif

#ifdef GAMMA_CORRECTION
uniform float gamma;
#endif

varying vec4 vertex;
varying float altitude;
void main()
{
    gl_FrontColor = gl_Color;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    vertex = gl_Vertex;
    altitude = texture2D(texture, gl_MultiTexCoord0.xy).a;

#ifdef INTERPOLATION
    altitude = interpolate(texture, kernel_lut, gl_MultiTexCoord0.xy, pixel).a;
#endif

#ifdef ELEVATION
    vertex.z = altitude*elevation;
#endif

    gl_Position = gl_ModelViewProjectionMatrix*vertex;
}
