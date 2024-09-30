```
digraph DeepFaceLab {
    node[shape=box, style=filled];
    rankdir=LR;

    // Meme zone
    ImagePreprocessing [label="Image Preprocessing"];
    FaceSwapGenerator [label="Face Swap Generator"];
    MemeGenerator [label="Meme Generation"];

    // Collect facesets
    CelebrityFacesetCollector [label="Celebrity Faceset Collector"];
    CommunityForum [label="Community Forum"];

    // GitHub ISSUES
    IssueTemplate [label="Issue Template"];
    ExpectedBehavior [label="Expected Behavior"];
    ActualBehavior [label="Actual Behavior"];
    StepsToReproduce [label="Steps to Reproduce"];
    OtherInfo [label="Other Relevant Information"];

    // DeepFaceLab
    DeepFaceLab [label="DeepFaceLab"];

    // Relationships
    ImagePreprocessing ->> FaceSwapGenerator;
    FaceSwapGenerator ->> MemeGenerator;
    CelebrityFacesetCollector ->> CommunityForum;
    IssueTemplate ->> ExpectedBehavior;
    ActualBehavior ->> StepsToReproduce;
    OtherInfo ->> ExpectedBehavior;

    // Subgraphs
    subgraph "Meme Generation" {
        ImagePreprocessing [label="Image Preprocessing"];
        FaceSwapGenerator [label="Face Swap Generator"];
        MemeGenerator [label="Meme Generation"];
    }
    
    subgraph "GitHub ISSUES" {
        IssueTemplate [label="Issue Template"];
        ExpectedBehavior [label="Expected Behavior"];
        ActualBehavior [label="Actual Behavior"];
        StepsToReproduce [label="Steps to Reproduce"];
        OtherInfo [label="Other Relevant Information"];
    }

    // Styles
    style[deepfacelab = color="#00698f", shape=ellipse];
}
```