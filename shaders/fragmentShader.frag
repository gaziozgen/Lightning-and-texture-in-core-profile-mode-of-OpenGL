#version 330

in vec4 fragColor;
in vec2 fragUV;
in vec3 fragPos;
in vec3 fragNormal;

out vec4 outColor;

uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float ratio;

uniform bool isSpec;
uniform vec3 viewPosition;

uniform vec3 directionalLightDir;
uniform vec4 directionalLightColor;
uniform float directionalLightIntensity;

uniform vec3 pointLightPos;
uniform vec4 pointLightColor;
uniform float pointLightIntensity;

uniform vec3  spotlightPosition;
uniform vec3  spotlightDirection;
uniform float innerCuttOffLocation;
uniform float outherCuttOffLocation;
uniform vec4 spotlightColor;
uniform float spotlightIntensity;

void main()
{

    vec4 texVal1 = texture(tex1, fragUV);
    vec4 texVal2 = texture(tex2, fragUV);
    vec4 texture = (((1 - ratio) * texVal1) + (ratio * texVal2));

    vec3 viewDir;
    vec3 halfwayDir;
    float spec;

    // directional light
    vec3 lightDir = normalize(-directionalLightDir);
    float diff = max(dot(fragNormal, lightDir), 0.0);
    if (isSpec){
        viewDir    = normalize(viewPosition - fragPos);
        halfwayDir = normalize(lightDir + viewDir);
        spec = pow(max(dot(fragNormal, halfwayDir), 0.0), 300.0);
    }
    vec4 directionalLight = directionalLightColor * directionalLightIntensity * (diff + spec);

    // point light
    lightDir = normalize(pointLightPos - fragPos);
    diff = max(dot(fragNormal, lightDir), 0.0);
    if (isSpec){
        viewDir    = normalize(viewPosition - fragPos);
        halfwayDir = normalize(lightDir + viewDir);
        spec = pow(max(dot(fragNormal, halfwayDir), 0.0), 300.0);
    }
    vec4 pointLight = pointLightColor * pointLightIntensity * (diff + spec);

    // spot light
    vec4 spotlight = vec4(0, 0, 0, 0);
    lightDir = normalize(spotlightPosition - fragPos);
    float theta = dot(lightDir, normalize(-spotlightDirection));
    if (theta > outherCuttOffLocation)
    {
        lightDir = normalize(spotlightPosition - fragPos);
        diff = max(dot(fragNormal, lightDir), 0.0);

        float epsilon = (innerCuttOffLocation - outherCuttOffLocation);
        float intensity = clamp((theta - outherCuttOffLocation) / epsilon, 0.0, 1.0);

        if (isSpec){
            viewDir    = normalize(viewPosition - fragPos);
            halfwayDir = normalize(lightDir + viewDir);
            spec = pow(max(dot(fragNormal, halfwayDir), 0.0), 300.0);
        }

        spotlight = spotlightColor * spotlightIntensity * intensity * (diff + spec);
    }

    outColor = texture * (pointLight + directionalLight + spotlight);
}